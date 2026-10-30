"""Tamil Nadu Class 10 (SSLC / Matriculation) Science: original practice questions, one list per textbook unit.

Same row format as maths.py: (unit code, question, correct answer, [three wrong answers], short explanation, difficulty). Units 1 to 22 follow the TN Class 10 Science textbook
(English medium): Physics 1 to 6, Chemistry 7 to 11, Biology 12 to 22. Unit 23 (Visual Communication) is not part of the written paper and is left out.
Facts are standard textbook facts; where a value depends on the convention (for example the speed of sound) the question avoids it.
"""

UNITS = [
    ('S1', 'Laws of Motion'), ('S2', 'Optics'), ('S3', 'Thermal Physics'), ('S4', 'Electricity'), ('S5', 'Acoustics'), ('S6', 'Nuclear Physics'),
    ('S7', 'Atoms and Molecules'), ('S8', 'Periodic Classification of Elements'), ('S9', 'Solutions'), ('S10', 'Types of Chemical Reactions'), ('S11', 'Carbon and its Compounds'),
    ('S12', 'Plant Anatomy and Plant Physiology'), ('S13', 'Structural Organisation of Animals'), ('S14', 'Transportation in Plants and Circulation in Animals'),
    ('S15', 'Nervous System'), ('S16', 'Plant and Animal Hormones'), ('S17', 'Reproduction in Plants and Animals'), ('S18', 'Genetics'),
    ('S19', 'Origin and Evolution of Life'), ('S20', 'Breeding and Biotechnology'), ('S21', 'Health and Diseases'), ('S22', 'Environmental Management'),
]

Q = [
    # ---- Unit 1 Laws of Motion
    ('S1', 'The SI unit of force is', 'newton (N)', ['kg m/s', 'joule (J)', 'watt (W)'], '1 N = 1 kg m/s², the force that gives 1 kg an acceleration of 1 m/s².', 1),
    ('S1', 'A force of 10 N acts on a body of mass 2 kg. The acceleration produced is', '5 m/s²', ['20 m/s²', '0.2 m/s²', '12 m/s²'], 'a = F/m = 10/2 = 5 m/s².', 1),
    ('S1', 'The momentum of a 2 kg body moving at 5 m/s is', '10 kg m/s', ['7 kg m/s', '2.5 kg m/s', '25 kg m/s'], 'Momentum = mass × velocity = 2 × 5.', 1),
    ('S1', 'A rocket moves upwards by throwing hot gases downwards. This is an example of', 'Newton’s third law', ['Newton’s first law', 'the law of inertia', 'Newton’s law of gravitation'], 'Action and reaction are equal and opposite.', 1),
    ('S1', 'If the distance between two masses is doubled, the gravitational force between them becomes', 'one-fourth', ['half', 'double', 'four times'], 'F is proportional to 1/r², so doubling r divides F by 4.', 2),
    ('S1', 'The approximate value of the acceleration due to gravity on the Earth’s surface is', '9.8 m/s²', ['6.67 m/s²', '1.6 m/s²', '98 m/s²'], 'g ≈ 9.8 m/s².', 1),
    ('S1', 'A man has a mass of 60 kg on the Earth. On the Moon his mass will be', '60 kg', ['10 kg', '360 kg', '0 kg'], 'Mass does not change with place; only weight does.', 2),
    ('S1', 'When a moving bus suddenly stops, the passengers lean forward. This is due to', 'inertia of motion', ['inertia of rest', 'inertia of direction', 'gravity'], 'The body tends to keep moving with its original motion.', 1),
    ('S1', 'In an isolated system, the total momentum before a collision is', 'equal to the total momentum after it', ['greater than after', 'less than after', 'always zero'], 'This is the law of conservation of linear momentum.', 2),

    # ---- Unit 2 Optics
    ('S2', 'The refractive index of a medium is the ratio of', 'the speed of light in vacuum to its speed in the medium', ['the speed of light in the medium to that in vacuum', 'the angle of incidence to the angle of reflection', 'the wavelength to the frequency'], 'n = c/v.', 1),
    ('S2', 'The power of a convex lens of focal length 50 cm is', '+2 D', ['+0.5 D', '+50 D', '−2 D'], 'P = 1/f in metres = 1/0.5 = 2 D; a convex lens has positive power.', 2),
    ('S2', 'Myopia (short-sightedness) is corrected using', 'a concave lens', ['a convex lens', 'a plane mirror', 'a bifocal prism'], 'A diverging lens moves the image back onto the retina.', 1),
    ('S2', 'Hypermetropia (long-sightedness) is corrected using', 'a convex lens', ['a concave lens', 'a cylindrical lens', 'a plane glass slab'], 'A converging lens brings the image forward onto the retina.', 1),
    ('S2', 'Total internal reflection can occur when light travels from', 'a denser medium to a rarer medium at an angle greater than the critical angle', ['a rarer medium to a denser medium at any angle', 'a denser medium to a rarer medium at an angle less than the critical angle', 'a rarer medium to a denser medium at a large angle'], 'Both conditions are needed.', 2),
    ('S2', 'When white light passes through a prism it splits into', 'seven colours', ['three colours', 'five colours', 'two colours'], 'VIBGYOR: violet, indigo, blue, green, yellow, orange, red.', 1),
    ('S2', 'The sky appears blue mainly because of', 'scattering of light by air molecules', ['reflection by the sea', 'absorption by clouds', 'dispersion by dust only'], 'Shorter (blue) wavelengths are scattered most.', 2),
    ('S2', 'When an object is placed at 2F of a convex lens, the image formed is', 'real, inverted and the same size, at 2F on the other side', ['virtual, erect and magnified', 'real, inverted and magnified, beyond 2F', 'real, erect and diminished'], 'At 2F the image is at 2F, with magnification −1.', 3),

    # ---- Unit 3 Thermal Physics
    ('S3', 'The SI unit of temperature is', 'kelvin', ['degree Celsius', 'degree Fahrenheit', 'joule'], 'The kelvin (K) is the SI base unit of temperature.', 1),
    ('S3', 'Absolute zero (0 K) is equal to about', '−273 °C', ['0 °C', '−100 °C', '273 °C'], '0 K = −273.15 °C.', 1),
    ('S3', 'Boyle’s law states that at constant temperature, the pressure of a fixed mass of gas is', 'inversely proportional to its volume', ['directly proportional to its volume', 'directly proportional to the square of its volume', 'independent of its volume'], 'PV = constant.', 1),
    ('S3', 'Charles’s law states that at constant pressure the volume of a fixed mass of gas is', 'directly proportional to its absolute temperature', ['inversely proportional to its absolute temperature', 'independent of temperature', 'directly proportional to its pressure'], 'V/T = constant, with T in kelvin.', 1),
    ('S3', 'A gas of volume 2 litres at 1 atm is compressed to 1 litre at constant temperature. Its new pressure is', '2 atm', ['0.5 atm', '1 atm', '4 atm'], 'P₁V₁ = P₂V₂ gives P₂ = 2 atm.', 2),
    ('S3', 'The ideal gas equation is', 'PV = nRT', ['PV = nR/T', 'P = nRTV', 'PT = nRV'], 'It combines Boyle’s, Charles’s and Avogadro’s laws.', 1),
    ('S3', 'The value of the universal gas constant R is approximately', '8.314 J mol⁻¹ K⁻¹', ['6.022 J mol⁻¹ K⁻¹', '9.8 J mol⁻¹ K⁻¹', '22.4 J mol⁻¹ K⁻¹'], 'R = 8.314 J/(mol K).', 2),
    ('S3', 'Avogadro’s law states that equal volumes of all gases at the same temperature and pressure contain', 'the same number of molecules', ['the same mass', 'the same number of atoms', 'the same density'], 'This is the statement of Avogadro’s law.', 1),

    # ---- Unit 4 Electricity
    ('S4', 'Ohm’s law states that at constant temperature the current through a conductor is', 'directly proportional to the potential difference across it', ['inversely proportional to the potential difference', 'independent of the potential difference', 'proportional to the square of the resistance'], 'V = IR.', 1),
    ('S4', 'The SI unit of resistivity is', 'ohm metre (Ω m)', ['ohm (Ω)', 'ohm per metre', 'siemens'], 'ρ = RA/l has the unit Ω m.', 2),
    ('S4', 'Two resistors of 2 Ω and 3 Ω are connected in series. The equivalent resistance is', '5 Ω', ['1.2 Ω', '6 Ω', '0.83 Ω'], 'In series the resistances add.', 1),
    ('S4', 'Two resistors of 2 Ω and 3 Ω are connected in parallel. The equivalent resistance is', '1.2 Ω', ['5 Ω', '6 Ω', '2.5 Ω'], '1/R = 1/2 + 1/3 = 5/6, so R = 1.2 Ω.', 2),
    ('S4', 'The power of an appliance that draws 5 A from a 220 V supply is', '1100 W', ['44 W', '225 W', '110 W'], 'P = VI = 220 × 5.', 1),
    ('S4', 'The heat produced in a resistor is given by Joule’s law as', 'H = I²Rt', ['H = IR/t', 'H = V/Rt', 'H = IRt²'], 'Heat is proportional to I², R and t.', 1),
    ('S4', 'The charge that flows when a current of 2 A passes for 10 s is', '20 C', ['5 C', '12 C', '0.2 C'], 'Q = It = 2 × 10.', 1),
    ('S4', 'In domestic wiring the electrical appliances are connected in', 'parallel', ['series', 'series and parallel alternately', 'a loop with no supply'], 'Each appliance then gets the full supply voltage and works independently.', 1),
    ('S4', 'A fuse wire is made of a material that has', 'a low melting point', ['a high melting point', 'very high resistance', 'a high boiling point'], 'It melts and breaks the circuit when the current is too high.', 1),
    ('S4', 'One kilowatt hour (kWh) is equal to', '3.6 × 10⁶ J', ['3.6 × 10³ J', '1000 J', '6 × 10⁶ J'], '1000 W × 3600 s = 3.6 × 10⁶ J.', 2),

    # ---- Unit 5 Acoustics
    ('S5', 'Sound waves cannot travel through', 'a vacuum', ['water', 'steel', 'air'], 'Sound needs a material medium.', 1),
    ('S5', 'The range of frequencies audible to a normal human ear is about', '20 Hz to 20 000 Hz', ['2 Hz to 200 Hz', '20 000 Hz to 200 000 Hz', '0 Hz to 20 Hz'], 'Below 20 Hz is infrasonic and above 20 kHz is ultrasonic.', 1),
    ('S5', 'A wave has frequency 500 Hz and wavelength 0.68 m. Its speed is', '340 m/s', ['736 m/s', '0.00136 m/s', '170 m/s'], 'v = fλ = 500 × 0.68.', 2),
    ('S5', 'Sound travels fastest in a', 'solid', ['gas', 'liquid', 'vacuum'], 'Particles are closest in solids, so the disturbance passes on quickest.', 1),
    ('S5', 'The loudness of a sound depends on its', 'amplitude', ['frequency', 'wavelength', 'speed'], 'A larger amplitude carries more energy and sounds louder.', 1),
    ('S5', 'The pitch of a sound depends on its', 'frequency', ['amplitude', 'speed in air', 'loudness'], 'Higher frequency means a higher pitch.', 1),
    ('S5', 'Sound waves of frequency above 20 000 Hz are called', 'ultrasonic waves', ['infrasonic waves', 'audible waves', 'seismic waves'], 'They are beyond the range of human hearing.', 1),
    ('S5', 'SONAR is a device that uses', 'ultrasonic waves to find the depth of the sea', ['infrasonic waves to measure speed of ships', 'X-rays to find fish', 'radio waves to hear underwater'], 'The echo of ultrasound gives the distance of an underwater object.', 2),

    # ---- Unit 6 Nuclear Physics
    ('S6', 'Radioactivity was discovered by', 'Henri Becquerel', ['Marie Curie', 'J. J. Thomson', 'James Chadwick'], 'Becquerel discovered it in 1896 while studying uranium salts.', 1),
    ('S6', 'An alpha particle is the nucleus of', 'a helium atom', ['a hydrogen atom', 'a lithium atom', 'an oxygen atom'], 'It has 2 protons and 2 neutrons.', 1),
    ('S6', 'The order of penetrating power of the radiations is', 'gamma > beta > alpha', ['alpha > beta > gamma', 'beta > gamma > alpha', 'alpha > gamma > beta'], 'Gamma rays pass through several centimetres of lead; alpha is stopped by paper.', 1),
    ('S6', 'Gamma rays are', 'electromagnetic waves with no charge', ['fast electrons', 'helium nuclei', 'neutrons'], 'They are high-energy photons.', 1),
    ('S6', 'The energy of the Sun is produced by', 'nuclear fusion', ['nuclear fission', 'burning of coal', 'chemical reaction of hydrogen with oxygen'], 'Hydrogen nuclei fuse to form helium.', 1),
    ('S6', 'In a nuclear reactor the chain reaction is controlled by', 'control rods such as cadmium or boron', ['the moderator', 'the coolant', 'the shielding wall'], 'Control rods absorb excess neutrons.', 2),
    ('S6', 'A radioactive sample of 80 g has a half-life of 2 days. The amount left after 4 days is', '20 g', ['40 g', '10 g', '0 g'], 'After 2 days 40 g, after 4 days 20 g.', 2),
    ('S6', 'The relation between mass and energy is', 'E = mc²', ['E = mc', 'E = m²c', 'E = mv²'], 'Einstein’s mass-energy equivalence.', 1),
    ('S6', 'The SI unit of radioactivity is', 'becquerel', ['curie', 'roentgen', 'sievert'], '1 becquerel is one disintegration per second.', 2),

    # ---- Unit 7 Atoms and Molecules
    ('S7', 'The value of Avogadro’s number is', '6.022 × 10²³', ['6.022 × 10²²', '3.011 × 10²³', '9.1 × 10⁻³¹'], 'One mole contains 6.022 × 10²³ particles.', 1),
    ('S7', 'The volume occupied by one mole of any gas at STP is', '22.4 litres', ['11.2 litres', '24 litres', '1 litre'], 'This is the molar volume at standard temperature and pressure.', 1),
    ('S7', 'The number of moles in 36 g of water (H₂O, molar mass 18 g/mol) is', '2', ['1', '0.5', '18'], '36 / 18 = 2.', 1),
    ('S7', 'The number of molecules in 0.5 mole of a substance is', '3.011 × 10²³', ['6.022 × 10²³', '1.2 × 10²⁴', '3.011 × 10²²'], '0.5 × 6.022 × 10²³.', 2),
    ('S7', 'The molecular mass of carbon dioxide (C = 12, O = 16) is', '44', ['28', '32', '56'], '12 + 2 × 16 = 44.', 1),
    ('S7', 'One atomic mass unit is defined as', '1/12 of the mass of a carbon-12 atom', ['the mass of a hydrogen molecule', 'the mass of one proton plus one electron', '1/16 of the mass of an oxygen molecule'], 'The carbon-12 scale is the standard.', 2),
    ('S7', 'The mass of 2 moles of sodium chloride (Na = 23, Cl = 35.5) is', '117 g', ['58.5 g', '35.5 g', '234 g'], '2 × 58.5 = 117.', 2),
    ('S7', 'The law of conservation of mass was stated by', 'Lavoisier', ['Dalton', 'Proust', 'Avogadro'], 'In a chemical reaction mass is neither created nor destroyed.', 1),
    ('S7', 'The gram atomic mass of oxygen is', '16 g', ['8 g', '32 g', '1 g'], 'Atomic mass of oxygen is 16 u, so one mole of atoms weighs 16 g.', 1),

    # ---- Unit 8 Periodic Classification of Elements
    ('S8', 'The modern periodic law states that the properties of elements are a periodic function of their', 'atomic numbers', ['atomic masses', 'densities', 'number of neutrons'], 'The modern law is based on atomic number (Moseley).', 1),
    ('S8', 'The modern periodic table has', '18 groups and 7 periods', ['8 groups and 7 periods', '18 groups and 8 periods', '16 groups and 7 periods'], 'This is the long form of the periodic table.', 1),
    ('S8', 'Elements in the same group have the same', 'number of valence electrons', ['atomic number', 'number of shells', 'atomic mass'], 'This gives them similar chemical properties.', 1),
    ('S8', 'The halogens belong to group', '17', ['1', '2', '18'], 'Fluorine, chlorine, bromine, iodine and astatine form group 17.', 1),
    ('S8', 'The noble gases belong to group', '18', ['17', '16', '1'], 'They have completely filled outer shells.', 1),
    ('S8', 'Moving from left to right across a period, the atomic radius generally', 'decreases', ['increases', 'stays the same', 'first increases then decreases'], 'The nuclear charge increases while the number of shells stays the same.', 2),
    ('S8', 'Moving down a group, the atomic radius', 'increases', ['decreases', 'remains constant', 'becomes zero'], 'Extra shells are added.', 1),
    ('S8', 'The most electronegative element is', 'fluorine', ['oxygen', 'chlorine', 'caesium'], 'Fluorine has the highest tendency to attract electrons.', 2),
    ('S8', 'Mendeleev arranged the elements in order of increasing', 'atomic mass', ['atomic number', 'density', 'valency'], 'His periodic law was based on atomic mass.', 1),

    # ---- Unit 9 Solutions
    ('S9', 'A solution is a', 'homogeneous mixture of two or more substances', ['heterogeneous mixture', 'compound with fixed composition', 'pure substance'], 'The components are uniformly mixed.', 1),
    ('S9', 'In a solution of sugar in water, water is the', 'solvent', ['solute', 'precipitate', 'solution'], 'The component present in the larger amount, which does the dissolving.', 1),
    ('S9', 'A saturated solution is one in which', 'no more solute can dissolve at that temperature', ['more solute can dissolve', 'there is no solute', 'the solvent is absent'], 'It holds the maximum amount of solute at that temperature.', 1),
    ('S9', 'The solubility of most solids in water', 'increases with an increase in temperature', ['decreases with an increase in temperature', 'does not depend on temperature', 'becomes zero on heating'], 'For most solids, heating dissolves more.', 1),
    ('S9', '10 g of salt is dissolved in 90 g of water. The percentage by mass of the solute is', '10%', ['9%', '11.1%', '90%'], '10 / (10 + 90) × 100 = 10%.', 2),
    ('S9', 'An aerated drink is an example of a solution of', 'a gas in a liquid', ['a liquid in a gas', 'a solid in a liquid', 'a gas in a solid'], 'Carbon dioxide is dissolved in water.', 1),
    ('S9', 'Brass is an example of', 'a solid solution (alloy)', ['a liquid solution', 'a gaseous solution', 'a compound'], 'It is a homogeneous mixture of copper and zinc.', 1),
    ('S9', 'Copper sulphate crystals are blue because they contain', 'water of crystallisation', ['copper only', 'sulphur only', 'no water at all'], 'On heating, the water is lost and the colour changes to white.', 2),
    ('S9', 'Washing soda crystals lose water of crystallisation on exposure to air. This property is called', 'efflorescence', ['deliquescence', 'hygroscopy', 'crystallisation'], 'Deliquescent substances absorb moisture; efflorescent ones lose it.', 2),

    # ---- Unit 10 Types of Chemical Reactions
    ('S10', '2H₂ + O₂ → 2H₂O is an example of a', 'combination reaction', ['decomposition reaction', 'displacement reaction', 'double displacement reaction'], 'Two substances combine to form one product.', 1),
    ('S10', 'CaCO₃ → CaO + CO₂ on heating is a', 'decomposition reaction', ['combination reaction', 'displacement reaction', 'neutralisation reaction'], 'One compound breaks into simpler substances.', 1),
    ('S10', 'Zn + CuSO₄ → ZnSO₄ + Cu is a', 'displacement reaction', ['combination reaction', 'decomposition reaction', 'precipitation reaction'], 'Zinc, a more reactive metal, displaces copper.', 1),
    ('S10', 'The reaction of an acid with a base to form salt and water is called', 'neutralisation', ['oxidation', 'decomposition', 'displacement'], 'For example HCl + NaOH → NaCl + H₂O.', 1),
    ('S10', 'The pH of a neutral solution at 25 °C is', '7', ['0', '14', '1'], 'Acids have pH below 7 and bases above 7.', 1),
    ('S10', 'Lemon juice has a pH of about 2. It is', 'acidic', ['basic', 'neutral', 'a salt'], 'pH below 7 means acidic.', 1),
    ('S10', 'A catalyst', 'changes the rate of a reaction without being used up', ['is always consumed', 'changes the products of a reaction', 'stops every reaction'], 'It provides a different path for the reaction.', 1),
    ('S10', 'Which of these does NOT increase the rate of a reaction?', 'lowering the temperature', ['raising the temperature', 'increasing the concentration of reactants', 'powdering a solid reactant'], 'A lower temperature slows the reaction.', 2),
    ('S10', 'The pH of a 0.01 M solution of the strong acid HCl is', '2', ['1', '7', '0.01'], 'pH = −log[H⁺] = −log(10⁻²) = 2.', 3),

    # ---- Unit 11 Carbon and its Compounds
    ('S11', 'The valency of carbon is', '4', ['2', '3', '1'], 'Carbon has four valence electrons and forms four covalent bonds.', 1),
    ('S11', 'The ability of carbon to form long chains with itself is called', 'catenation', ['isomerism', 'polymerisation', 'allotropy'], 'It gives rise to the huge number of carbon compounds.', 1),
    ('S11', 'The general formula of alkanes is', 'CₙH₂ₙ₊₂', ['CₙH₂ₙ', 'CₙH₂ₙ₋₂', 'CₙHₙ'], 'For example methane CH₄ (n = 1) and ethane C₂H₆ (n = 2).', 1),
    ('S11', 'Ethene (C₂H₄) contains', 'a carbon-carbon double bond', ['a carbon-carbon single bond only', 'a carbon-carbon triple bond', 'no carbon-carbon bond'], 'It is an alkene.', 1),
    ('S11', 'The functional group of carboxylic acids is', '–COOH', ['–OH', '–CHO', '–CO–'], '–OH is alcohol, –CHO is aldehyde and –CO– is ketone.', 1),
    ('S11', 'The IUPAC name of CH₃CH₂OH is', 'ethanol', ['methanol', 'ethanal', 'ethanoic acid'], 'Two carbons (eth-) with the –OH group (-ol).', 1),
    ('S11', 'The reaction of a carboxylic acid with an alcohol to form a sweet-smelling compound is called', 'esterification', ['saponification', 'hydrogenation', 'combustion'], 'The product is an ester.', 2),
    ('S11', 'Soaps are', 'sodium or potassium salts of long-chain fatty acids', ['esters of glycerol', 'hydrocarbons', 'alcohols'], 'They are made by saponification of fats and oils.', 2),
    ('S11', 'Compounds with the same molecular formula but different structures are called', 'isomers', ['isotopes', 'allotropes', 'isobars'], 'For example butane and isobutane (C₄H₁₀).', 1),

    # ---- Unit 12 Plant Anatomy and Plant Physiology
    ('S12', 'The tissue responsible for growth in length of a plant is', 'apical meristem', ['lateral meristem', 'collenchyma', 'sclerenchyma'], 'Apical meristems at the tips of roots and shoots increase length.', 1),
    ('S12', 'Water and minerals are conducted upwards through the', 'xylem', ['phloem', 'cambium', 'epidermis'], 'Xylem carries water; phloem carries food.', 1),
    ('S12', 'Food prepared in the leaves is transported to other parts through the', 'phloem', ['xylem', 'root hairs', 'stomata'], 'This is translocation.', 1),
    ('S12', 'Gaseous exchange in leaves takes place through the', 'stomata', ['cuticle', 'veins', 'root hairs'], 'Stomata are pores surrounded by guard cells.', 1),
    ('S12', 'The site of photosynthesis in a plant cell is the', 'chloroplast', ['mitochondrion', 'nucleus', 'ribosome'], 'Chloroplasts contain chlorophyll.', 1),
    ('S12', 'The balanced equation for photosynthesis is', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂ (in sunlight, with chlorophyll)', ['C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', '6CO₂ + 6O₂ → C₆H₁₂O₆ + 6H₂O', 'CO₂ + H₂O → C + O₂'], 'Carbon dioxide and water form glucose and oxygen.', 2),
    ('S12', 'The loss of water vapour from the aerial parts of a plant is called', 'transpiration', ['translocation', 'guttation', 'respiration'], 'Most of it happens through the stomata.', 1),
    ('S12', 'The vascular bundles of a monocot stem are', 'scattered and closed (without cambium)', ['arranged in a ring and open', 'absent', 'arranged in a ring and closed'], 'Monocots therefore show no secondary growth.', 2),
    ('S12', 'Glycolysis, the first step of respiration, takes place in the', 'cytoplasm', ['mitochondria', 'nucleus', 'chloroplast'], 'It breaks glucose into pyruvic acid.', 2),

    # ---- Unit 13 Structural Organisation of Animals
    ('S13', 'The tissue that covers the body surface and lines the body cavities is', 'epithelial tissue', ['connective tissue', 'muscular tissue', 'nervous tissue'], 'It forms protective and lining layers.', 1),
    ('S13', 'Blood, bone and cartilage are examples of', 'connective tissue', ['epithelial tissue', 'muscular tissue', 'nervous tissue'], 'They connect and support other tissues.', 1),
    ('S13', 'Which muscle is striated and involuntary?', 'cardiac muscle', ['skeletal muscle', 'smooth muscle', 'none of these'], 'Cardiac muscle is found only in the heart.', 2),
    ('S13', 'The muscles of the stomach and intestine are', 'smooth and involuntary', ['striated and voluntary', 'striated and involuntary', 'smooth and voluntary'], 'They work without conscious control.', 1),
    ('S13', 'Muscles are connected to bones by', 'tendons', ['ligaments', 'cartilage', 'nerves'], 'Ligaments connect bone to bone.', 1),
    ('S13', 'Adipose tissue is a connective tissue that', 'stores fat', ['carries oxygen', 'transmits impulses', 'covers the skin'], 'Fat stores energy and insulates the body.', 1),
    ('S13', 'The functional unit of nervous tissue is the', 'neuron', ['nephron', 'sarcomere', 'osteocyte'], 'Neurons carry electrical impulses.', 1),
    ('S13', 'Red blood cells carry oxygen with the help of', 'haemoglobin', ['plasma', 'platelets', 'lymph'], 'Haemoglobin is an iron-containing pigment.', 1),

    # ---- Unit 14 Transportation in Plants and Circulation in Animals
    ('S14', 'The upward movement of water in tall trees is mainly due to', 'transpiration pull', ['gravity', 'phloem pressure', 'cell division'], 'Water is pulled up the xylem as it evaporates from the leaves.', 2),
    ('S14', 'The human heart has', 'four chambers', ['two chambers', 'three chambers', 'five chambers'], 'Two atria and two ventricles.', 1),
    ('S14', 'The blood vessels that carry blood away from the heart are', 'arteries', ['veins', 'capillaries', 'lymph vessels'], 'Arteries have thick, elastic walls.', 1),
    ('S14', 'The pulmonary artery carries', 'deoxygenated blood from the heart to the lungs', ['oxygenated blood to the lungs', 'oxygenated blood to the body', 'deoxygenated blood from the body'], 'It is the only artery carrying deoxygenated blood.', 3),
    ('S14', 'The blood group called the universal donor is', 'O negative', ['AB positive', 'A positive', 'B negative'], 'It has no A, B or Rh antigens.', 2),
    ('S14', 'The normal blood pressure of a healthy adult is about', '120/80 mm Hg', ['80/120 mm Hg', '200/100 mm Hg', '60/40 mm Hg'], 'Systolic over diastolic pressure.', 1),
    ('S14', 'Human beings have double circulation. This means that blood passes through the heart', 'twice in one complete circuit of the body', ['once in one complete circuit', 'three times in one circuit', 'only in the lungs'], 'Pulmonary and systemic circulation.', 2),
    ('S14', 'The natural pacemaker of the heart is the', 'sino-atrial (SA) node', ['atrioventricular node', 'aorta', 'bundle of His'], 'It starts each heartbeat.', 2),

    # ---- Unit 15 Nervous System
    ('S15', 'The structural and functional unit of the nervous system is the', 'neuron', ['nephron', 'neutron', 'axon only'], 'A neuron has a cell body, dendrites and an axon.', 1),
    ('S15', 'In a neuron, the impulse is received by the', 'dendrites', ['axon', 'myelin sheath', 'synapse'], 'The axon carries it away from the cell body.', 1),
    ('S15', 'The correct sequence of a reflex arc is', 'receptor → sensory neuron → spinal cord → motor neuron → effector', ['receptor → motor neuron → brain → sensory neuron → effector', 'effector → sensory neuron → spinal cord → motor neuron → receptor', 'sensory neuron → receptor → effector → spinal cord'], 'The spinal cord acts as the centre for a simple reflex.', 2),
    ('S15', 'The part of the brain that controls balance and posture is the', 'cerebellum', ['cerebrum', 'medulla oblongata', 'hypothalamus'], 'It coordinates voluntary movements.', 1),
    ('S15', 'Involuntary actions such as breathing and heartbeat are controlled by the', 'medulla oblongata', ['cerebrum', 'cerebellum', 'pituitary'], 'It is part of the hindbrain.', 2),
    ('S15', 'The central nervous system consists of', 'the brain and the spinal cord', ['the brain and the nerves', 'the spinal cord and the nerves', 'all the sense organs'], 'Nerves belong to the peripheral nervous system.', 1),
    ('S15', 'The gap between two neurons is called the', 'synapse', ['node of Ranvier', 'dendrite', 'myelin'], 'Chemical messengers cross it.', 1),
    ('S15', 'The body temperature is regulated by the', 'hypothalamus', ['cerebellum', 'spinal cord', 'cerebrum'], 'It acts like a thermostat.', 2),

    # ---- Unit 16 Plant and Animal Hormones
    ('S16', 'The plant hormone that promotes cell elongation and phototropism is', 'auxin', ['cytokinin', 'abscisic acid', 'ethylene'], 'Auxin collects on the shaded side of the stem.', 1),
    ('S16', 'The plant hormone that promotes fruit ripening is', 'ethylene', ['gibberellin', 'auxin', 'cytokinin'], 'It is a gas.', 1),
    ('S16', 'The plant hormone that promotes cell division is', 'cytokinin', ['auxin', 'abscisic acid', 'ethylene'], 'It works with auxin in tissue culture.', 2),
    ('S16', 'Abscisic acid is called the stress hormone because it', 'closes stomata and promotes dormancy', ['promotes stem elongation', 'ripens fruit', 'causes cell division'], 'It helps the plant survive dry conditions.', 2),
    ('S16', 'Deficiency of iodine in the diet causes', 'goitre', ['diabetes', 'dwarfism', 'scurvy'], 'Iodine is needed to make thyroxine.', 1),
    ('S16', 'Insulin is secreted by the', 'pancreas', ['liver', 'thyroid', 'adrenal gland'], 'It lowers blood glucose; its deficiency causes diabetes mellitus.', 1),
    ('S16', 'The hormone released during emergencies that prepares the body for fight or flight is', 'adrenaline', ['insulin', 'thyroxine', 'oestrogen'], 'It is secreted by the adrenal glands.', 1),
    ('S16', 'The gland called the master gland is the', 'pituitary gland', ['thyroid gland', 'pancreas', 'adrenal gland'], 'It controls many other endocrine glands.', 1),
    ('S16', 'The male sex hormone is', 'testosterone', ['oestrogen', 'progesterone', 'thyroxine'], 'It is secreted by the testes.', 1),

    # ---- Unit 17 Reproduction in Plants and Animals
    ('S17', 'Amoeba reproduces by', 'binary fission', ['budding', 'spore formation', 'fragmentation'], 'The parent cell divides into two equal daughter cells.', 1),
    ('S17', 'Hydra and yeast reproduce by', 'budding', ['binary fission', 'spore formation', 'regeneration only'], 'A small outgrowth develops into a new individual.', 1),
    ('S17', 'Growing a new plant from a rose stem cutting is an example of', 'vegetative propagation', ['sexual reproduction', 'budding in yeast', 'spore formation'], 'A part of the plant gives rise to a new plant.', 1),
    ('S17', 'The transfer of pollen from an anther to a stigma is called', 'pollination', ['fertilisation', 'germination', 'fruit formation'], 'It may be self-pollination or cross-pollination.', 1),
    ('S17', 'After fertilisation in a flower, the ovule develops into the', 'seed', ['fruit', 'petal', 'stamen'], 'The ovary becomes the fruit.', 1),
    ('S17', 'In human beings fertilisation normally takes place in the', 'fallopian tube (oviduct)', ['uterus', 'ovary', 'vagina'], 'The zygote then moves to the uterus.', 2),
    ('S17', 'The organ that supplies nutrients and oxygen to the developing embryo is the', 'placenta', ['ovary', 'testis', 'amnion'], 'It connects the embryo to the mother’s uterus wall.', 1),
    ('S17', 'Double fertilisation is a feature of', 'flowering plants', ['mosses', 'ferns', 'fish'], 'One male gamete fuses with the egg and the other with the polar nuclei.', 3),

    # ---- Unit 18 Genetics
    ('S18', 'The father of genetics is', 'Gregor Mendel', ['Charles Darwin', 'Louis Pasteur', 'Watson'], 'He worked on pea plants.', 1),
    ('S18', 'The phenotypic ratio in the F₂ generation of a monohybrid cross is', '3 : 1', ['1 : 1', '9 : 3 : 3 : 1', '1 : 2 : 1'], 'Three dominant for every one recessive.', 1),
    ('S18', 'The phenotypic ratio in the F₂ generation of a dihybrid cross is', '9 : 3 : 3 : 1', ['3 : 1', '1 : 2 : 1', '1 : 1 : 1 : 1'], 'Mendel’s law of independent assortment.', 1),
    ('S18', 'The genotypic ratio in the F₂ generation of a monohybrid cross is', '1 : 2 : 1', ['3 : 1', '9 : 3 : 3 : 1', '2 : 1'], 'TT : Tt : tt = 1 : 2 : 1.', 2),
    ('S18', 'The double helix model of DNA was proposed by', 'Watson and Crick', ['Mendel and Morgan', 'Darwin and Wallace', 'Miller and Urey'], 'In 1953.', 1),
    ('S18', 'In DNA, adenine pairs with', 'thymine', ['guanine', 'cytosine', 'uracil'], 'A pairs with T and G with C.', 1),
    ('S18', 'The number of chromosomes in a human body cell is', '46', ['23', '44', '48'], '23 pairs.', 1),
    ('S18', 'The sex of a human child is determined by the', 'sperm of the father', ['egg of the mother', 'age of the mother', 'blood group'], 'A sperm carries either X or Y; the egg always carries X.', 2),
    ('S18', 'An organism with the genotype Tt is called', 'heterozygous', ['homozygous dominant', 'homozygous recessive', 'a pure line'], 'It has two different alleles.', 1),

    # ---- Unit 19 Origin and Evolution of Life
    ('S19', 'The theory of natural selection was proposed by', 'Charles Darwin', ['Lamarck', 'Mendel', 'Hugo de Vries'], 'Presented in “On the Origin of Species”.', 1),
    ('S19', 'The forelimb of a human and the wing of a bat are examples of', 'homologous organs', ['analogous organs', 'vestigial organs', 'rudimentary organs'], 'Different functions, similar basic structure.', 1),
    ('S19', 'The wings of a bird and the wings of an insect are', 'analogous organs', ['homologous organs', 'vestigial organs', 'the same in structure'], 'Same function, different origin.', 1),
    ('S19', 'The study of fossils is called', 'palaeontology', ['embryology', 'ecology', 'taxonomy'], 'Fossils show how life has changed.', 1),
    ('S19', 'Archaeopteryx is considered a connecting link between', 'reptiles and birds', ['fish and amphibians', 'amphibians and reptiles', 'reptiles and mammals'], 'It had feathers and also teeth and a long tail.', 2),
    ('S19', 'The age of fossils is estimated using', 'carbon-14 dating', ['hydrogen dating', 'pH testing', 'litmus paper'], 'The half-life of carbon-14 is used for dating.', 2),
    ('S19', 'The appendix in human beings is an example of a', 'vestigial organ', ['homologous organ', 'analogous organ', 'fossil'], 'It has lost most of its function.', 1),
    ('S19', 'The Miller and Urey experiment demonstrated the', 'formation of simple organic molecules from inorganic gases', ['formation of cells from sunlight', 'origin of species', 'inheritance of acquired characters'], 'They passed electric sparks through a mixture of gases.', 3),

    # ---- Unit 20 Breeding and Biotechnology
    ('S20', 'Dolly the sheep was produced by', 'cloning using the nucleus of a body cell', ['cross-breeding with another sheep', 'artificial insemination', 'tissue culture of a leaf'], 'The nucleus of a mammary cell was transferred into an enucleated egg.', 1),
    ('S20', 'Growing a whole plant from a small piece of tissue in a nutrient medium is called', 'tissue culture', ['grafting', 'layering', 'budding'], 'It depends on totipotency of plant cells.', 1),
    ('S20', 'Bt cotton is resistant to insects because it contains a gene from', 'Bacillus thuringiensis', ['Rhizobium', 'Escherichia coli', 'Penicillium'], 'The gene produces a toxin harmful to certain pests.', 1),
    ('S20', 'Human insulin is produced commercially using', 'genetically modified bacteria', ['pig pancreas only', 'cow milk', 'plant roots'], 'The human insulin gene is inserted into bacteria such as E. coli.', 2),
    ('S20', 'The Green Revolution in India is associated with', 'M. S. Swaminathan and high yielding varieties', ['the white revolution', 'the blue revolution', 'the discovery of penicillin'], 'It increased the production of wheat and rice.', 1),
    ('S20', 'Which of these is a biofertiliser?', 'Rhizobium', ['urea', 'DDT', 'superphosphate'], 'It fixes atmospheric nitrogen in the root nodules of legumes.', 1),
    ('S20', 'Stem cells are special because they', 'can develop into many kinds of cells', ['cannot divide', 'are found only in plants', 'are always cancerous'], 'They are used in regenerative medicine.', 1),
    ('S20', 'Crossing two genetically different plants to get an improved variety is called', 'hybridisation', ['cloning', 'grafting', 'layering'], 'The offspring combines desirable traits of both parents.', 1),

    # ---- Unit 21 Health and Diseases
    ('S21', 'Malaria is caused by a', 'protozoan (Plasmodium) spread by the female Anopheles mosquito', ['virus spread by Aedes', 'bacterium spread by water', 'fungus spread by air'], 'The parasite is Plasmodium.', 1),
    ('S21', 'Dengue is spread by the mosquito', 'Aedes', ['Anopheles', 'Culex', 'housefly'], 'It is a viral disease.', 1),
    ('S21', 'Tuberculosis is caused by a', 'bacterium', ['virus', 'protozoan', 'fungus'], 'Mycobacterium tuberculosis.', 1),
    ('S21', 'The first vaccine, for smallpox, was developed by', 'Edward Jenner', ['Louis Pasteur', 'Alexander Fleming', 'Robert Koch'], 'He used cowpox material.', 1),
    ('S21', 'Penicillin was discovered by', 'Alexander Fleming', ['Edward Jenner', 'Robert Koch', 'Louis Pasteur'], 'It is an antibiotic obtained from the mould Penicillium.', 1),
    ('S21', 'AIDS is caused by', 'HIV', ['a bacterium', 'a protozoan', 'a fungus'], 'The virus attacks the helper T cells of the immune system.', 1),
    ('S21', 'Scurvy is caused by the deficiency of', 'vitamin C', ['vitamin A', 'vitamin D', 'vitamin K'], 'Citrus fruits prevent it.', 1),
    ('S21', 'Rickets is caused by the deficiency of', 'vitamin D', ['vitamin C', 'vitamin A', 'vitamin B₁₂'], 'It leads to weak, bent bones.', 1),
    ('S21', 'Cancer is caused by', 'uncontrolled division of cells', ['a bacterial infection', 'deficiency of iron', 'lack of vitamin A'], 'The cells form a mass called a tumour.', 1),

    # ---- Unit 22 Environmental Management
    ('S22', 'The gases mainly responsible for the greenhouse effect include', 'carbon dioxide and methane', ['oxygen and nitrogen', 'helium and neon', 'hydrogen and argon'], 'They trap heat in the atmosphere.', 1),
    ('S22', 'The ozone layer is mainly damaged by', 'chlorofluorocarbons (CFCs)', ['carbon dioxide', 'oxygen', 'water vapour'], 'CFCs release chlorine atoms that destroy ozone.', 1),
    ('S22', 'Acid rain is caused mainly by', 'oxides of sulphur and nitrogen', ['carbon monoxide', 'oxygen', 'argon'], 'They form sulphuric and nitric acids in the atmosphere.', 1),
    ('S22', 'The three Rs of waste management are', 'reduce, reuse and recycle', ['read, write and repeat', 'remove, rebuild and rest', 'replant, reduce and release'], 'They reduce the burden on the environment.', 1),
    ('S22', 'Which of these is non-biodegradable?', 'plastic', ['paper', 'vegetable peel', 'cotton cloth'], 'Plastic is not broken down by microorganisms.', 1),
    ('S22', 'Which of these is a biodiversity hotspot in India?', 'the Western Ghats', ['the Thar desert', 'the Deccan plateau', 'the Ganga plains'], 'It is rich in endemic species.', 2),
    ('S22', 'The Chipko movement was started to', 'protect trees from being cut', ['build dams', 'plant sugarcane', 'harvest rainwater'], 'Villagers hugged trees to save them.', 1),
    ('S22', 'Excessive nutrients such as fertiliser washed into a lake lead to', 'eutrophication', ['desertification', 'the greenhouse effect', 'ozone depletion'], 'Algae grow rapidly and use up the oxygen in the water.', 2),
    ('S22', 'The IUCN Red Data Book lists', 'species that are threatened with extinction', ['all the plants of a country', 'only extinct dinosaurs', 'medicinal plants'], 'It guides conservation action.', 2),
]
